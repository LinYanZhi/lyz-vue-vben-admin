<script lang="ts" setup>
import { onMounted, ref } from 'vue';

import { Page, useVbenDrawer } from '@vben/common-ui';

import { ElButton, ElMessage, ElMessageBox, ElTable } from 'element-plus';

import {
  createRoleApi,
  deleteRoleApi,
  getAllMenusApi,
  getRoleListApi,
  updateRoleApi,
} from '#/api';

// 表格数据
const tableData = ref<any[]>([]);
const loading = ref(false);
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
});

// 搜索条件
const searchForm = ref({
  name: '',
  code: '',
});

// 菜单树数据
const menuTreeData = ref<any[]>([]);

// 抽屉配置
const [drawer, { open, close }] = useVbenDrawer({
  title: '角色信息',
  width: 800,
});

// 表单配置
const [RoleForm, formApi] = useVbenForm({
  layout: 'vertical',
  handleSubmit: async (values) => {
    try {
      // 处理菜单权限
      const menuIds = extractMenuIds(values.menuIds);

      const params = {
        ...values,
        menuIds,
      };

      if (formApi.model.id) {
        await updateRoleApi(formApi.model.id, params);
        ElMessage.success('角色更新成功');
      } else {
        await createRoleApi(params);
        ElMessage.success('角色创建成功');
      }
      close();
      getList();
    } catch (error) {
      ElMessage.error('操作失败');
      console.error(error);
    }
  },
  schema: [
    {
      component: 'Input',
      fieldName: 'name',
      label: '角色名称',
      componentProps: {
        placeholder: '请输入角色名称',
        maxlength: 50,
      },
      rules: [
        { required: true, message: '请输入角色名称' },
        { min: 2, max: 50, message: '角色名称长度在 2 到 50 个字符' },
      ],
    },
    {
      component: 'Input',
      fieldName: 'code',
      label: '角色编码',
      componentProps: {
        placeholder: '请输入角色编码',
        maxlength: 50,
      },
      rules: [
        { required: true, message: '请输入角色编码' },
        { min: 2, max: 50, message: '角色编码长度在 2 到 50 个字符' },
      ],
    },
    {
      component: 'InputTextArea',
      fieldName: 'remark',
      label: '角色描述',
      componentProps: {
        placeholder: '请输入角色描述',
        maxlength: 200,
        rows: 3,
      },
    },
    {
      component: 'Switch',
      fieldName: 'status',
      label: '状态',
      componentProps: {
        trueValue: true,
        falseValue: false,
        defaultValue: true,
      },
    },
    {
      component: 'Tree',
      fieldName: 'menuIds',
      label: '菜单权限',
      componentProps: {
        data: menuTreeData,
        props: {
          label: 'title',
          value: 'id',
          children: 'children',
        },
        checkStrictly: false,
        showCheckbox: true,
        nodeKey: 'id',
      },
      rules: [{ required: true, message: '请选择菜单权限' }],
    },
  ],
});

// 提取菜单ID（包括所有选中的子菜单）
const extractMenuIds = (menuIds: number[]): number[] => {
  const allIds: number[] = [];

  const findChildIds = (node: any) => {
    allIds.push(node.id);
    if (node.children && node.children.length > 0) {
      node.children.forEach((child: any) => findChildIds(child));
    }
  };

  const traverseTree = (tree: any[]) => {
    tree.forEach((node) => {
      if (menuIds.includes(node.id)) {
        findChildIds(node);
      } else if (node.children && node.children.length > 0) {
        traverseTree(node.children);
      }
    });
  };

  traverseTree(menuTreeData.value);
  return [...new Set(allIds)];
};

// 从菜单数据中提取选中的ID
const getCheckedMenuIds = (menuIds: number[], tree: any[]): number[] => {
  const checkedIds: number[] = [];

  const traverseTree = (nodes: any[]) => {
    nodes.forEach((node) => {
      if (menuIds.includes(node.id)) {
        checkedIds.push(node.id);
      }
      if (node.children && node.children.length > 0) {
        traverseTree(node.children);
      }
    });
  };

  traverseTree(tree);
  return checkedIds;
};

// 获取角色列表
const getList = async () => {
  loading.value = true;
  try {
    const params = {
      ...searchForm.value,
      page: pagination.value.current,
      pageSize: pagination.value.pageSize,
    };
    const res = await getRoleListApi(params);
    tableData.value = res.data || [];
    pagination.value.total = res.total || 0;
  } catch (error) {
    console.error('获取角色列表失败', error);
  } finally {
    loading.value = false;
  }
};

// 获取所有菜单（树形结构）
const getAllMenus = async () => {
  try {
    const res = await getAllMenusApi();
    menuTreeData.value = res.data || [];
  } catch (error) {
    console.error('获取菜单列表失败', error);
  }
};

// 打开新增抽屉
const handleAdd = () => {
  formApi.setValues({});
  drawer.title = '新增角色';
  open();
};

// 打开编辑抽屉
const handleEdit = async (row: any) => {
  // 设置表单值
  formApi.setValues({
    ...row,
    menuIds: getCheckedMenuIds(row.menuIds, menuTreeData.value),
  });
  drawer.title = '编辑角色';
  open();
};

// 删除角色
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    await deleteRoleApi([row.id]);
    ElMessage.success('删除成功');
    getList();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
      console.error(error);
    }
  }
};

// 批量删除
const selectedRows = ref<any[]>([]);
const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的角色');
    return;
  }
  try {
    await ElMessageBox.confirm('确定要删除选中的角色吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    const ids = selectedRows.value.map((row) => row.id);
    await deleteRoleApi(ids);
    ElMessage.success('批量删除成功');
    selectedRows.value = [];
    getList();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败');
      console.error(error);
    }
  }
};

// 搜索
const handleSearch = () => {
  pagination.value.current = 1;
  getList();
};

// 重置搜索
const handleReset = () => {
  searchForm.value = {
    name: '',
    code: '',
  };
  getList();
};

// 表格列配置
const columns = [
  {
    title: '角色名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '角色编码',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '角色描述',
    dataIndex: 'remark',
    key: 'remark',
    ellipsis: true,
    width: 300,
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100,
    render: (status: boolean) => {
      return status
        ? h('span', { class: 'text-green-500' }, '启用')
        : h('span', { class: 'text-red-500' }, '禁用');
    },
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 180,
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    fixed: 'right',
    width: 150,
    slotName: 'action',
  },
];

// 初始化数据
onMounted(() => {
  getList();
  getAllMenus();
});
</script>

<template>
  <Page>
    <template #header>
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-bold">角色管理</h1>
        <div class="flex space-x-2">
          <Button type="primary" @click="handleAdd">
            <template #icon>
              <i class="lucide:plus"></i>
            </template>
            新增
          </Button>
          <Button
            type="danger"
            @click="handleBatchDelete"
            :disabled="selectedRows.length === 0"
          >
            <template #icon>
              <i class="lucide:trash-2"></i>
            </template>
            批量删除
          </Button>
        </div>
      </div>
    </template>

    <div class="mt-4 rounded-lg bg-white p-4 shadow">
      <div class="mb-4 flex flex-wrap gap-4">
        <div class="w-full md:w-auto">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入角色名称"
            clearable
            @keyup.enter="handleSearch"
            class="w-64"
          >
            <template #prefix>
              <i class="lucide:tag"></i>
            </template>
          </el-input>
        </div>
        <div class="w-full md:w-auto">
          <el-input
            v-model="searchForm.code"
            placeholder="请输入角色编码"
            clearable
            @keyup.enter="handleSearch"
            class="w-64"
          >
            <template #prefix>
              <i class="lucide:code"></i>
            </template>
          </el-input>
        </div>
        <div class="flex w-full items-end md:w-auto">
          <Button type="primary" @click="handleSearch" class="mr-2">
            <template #icon>
              <i class="lucide:search"></i>
            </template>
            搜索
          </Button>
          <Button @click="handleReset">
            <template #icon>
              <i class="lucide:refresh-cw"></i>
            </template>
            重置
          </Button>
        </div>
      </div>

      <ElTable
        v-model:selected-rows="selectedRows"
        :columns="columns"
        :data-source="tableData"
        :loading="loading"
        :pagination="pagination"
        @pagination-change="getList"
        row-key="id"
      >
        <template #action="{ row }">
          <ElSpace size="small">
            <ElButton type="primary" link @click="handleEdit(row)">
              编辑
            </ElButton>
            <ElButton type="danger" link @click="handleDelete(row)">
              删除
            </ElButton>
          </ElSpace>
        </template>
      </ElTable>
    </div>

    <template #footer>
      <div class="text-center text-sm text-gray-500">
        显示第 {{ (pagination.current - 1) * pagination.pageSize + 1 }}-{{
          Math.min(pagination.current * pagination.pageSize, pagination.total)
        }}
        条，共 {{ pagination.total }} 条记录
      </div>
    </template>
  </Page>

  <drawer>
    <RoleForm />
  </drawer>
</template>
