<script lang="ts" setup>
import { h, onMounted, ref } from 'vue';

import { Page, useVbenDrawer } from '@vben/common-ui';

import { ElButton, ElMessage, ElMessageBox, ElTable } from 'element-plus';

import { useVbenForm } from '#/adapter/form';
import {
  createMenuApi,
  deleteMenuApi,
  getAllMenusApi,
  getMenuListApi,
  updateMenuApi,
} from '#/api';

// 表格数据
const tableData = ref<any[]>([]);
const treeData = ref<any[]>([]);
const loading = ref(false);
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
});

// 搜索条件
const searchForm = ref({
  title: '',
  status: undefined,
});

// 抽屉配置
const [drawer, { open, close }] = useVbenDrawer({
  title: '菜单信息',
  width: 600,
});

// 表单配置
const [Form, formApi] = useVbenForm({
  layout: 'vertical',
  handleSubmit: async (values) => {
    try {
      // 处理菜单类型为按钮时的特殊处理
      if (values.type === 2) {
        values.path = '';
        values.component = '';
      }

      if (formApi.model.id) {
        await updateMenuApi(formApi.model.id, values);
        ElMessage.success('菜单更新成功');
      } else {
        await createMenuApi(values);
        ElMessage.success('菜单创建成功');
      }
      close();
      getList();
      getAllMenus();
    } catch (error) {
      ElMessage.error('操作失败');
      console.error(error);
    }
  },
  schema: [
    {
      component: 'Select',
      fieldName: 'type',
      label: '菜单类型',
      componentProps: {
        placeholder: '请选择菜单类型',
        options: [
          { label: '目录', value: 0 },
          { label: '菜单', value: 1 },
          { label: '按钮', value: 2 },
        ],
      },
      rules: [{ required: true, message: '请选择菜单类型' }],
    },
    {
      component: 'TreeSelect',
      fieldName: 'parentId',
      label: '上级菜单',
      componentProps: {
        data: treeData,
        props: {
          label: 'title',
          value: 'id',
          children: 'children',
        },
        placeholder: '请选择上级菜单',
        allowClear: true,
      },
    },
    {
      component: 'Input',
      fieldName: 'title',
      label: '菜单名称',
      componentProps: {
        placeholder: '请输入菜单名称',
        maxlength: 50,
      },
      rules: [
        { required: true, message: '请输入菜单名称' },
        { min: 1, max: 50, message: '菜单名称长度在 1 到 50 个字符' },
      ],
    },
    {
      component: 'Input',
      fieldName: 'path',
      label: '路由路径',
      componentProps: {
        placeholder: '请输入路由路径',
        maxlength: 100,
      },
      rules: [
        {
          required: ({ model }) => model.type !== 2,
          message: '请输入路由路径',
        },
      ],
    },
    {
      component: 'Input',
      fieldName: 'name',
      label: '路由名称',
      componentProps: {
        placeholder: '请输入路由名称',
        maxlength: 50,
      },
    },
    {
      component: 'Input',
      fieldName: 'component',
      label: '组件路径',
      componentProps: {
        placeholder: '请输入组件路径',
        maxlength: 200,
      },
      rules: [
        {
          required: ({ model }) => model.type === 1,
          message: '请输入组件路径',
        },
      ],
    },
    {
      component: 'Input',
      fieldName: 'redirect',
      label: '重定向路径',
      componentProps: {
        placeholder: '请输入重定向路径',
        maxlength: 100,
      },
    },
    {
      component: 'Input',
      fieldName: 'icon',
      label: '菜单图标',
      componentProps: {
        placeholder: '请输入菜单图标',
        maxlength: 50,
      },
    },
    {
      component: 'InputNumber',
      fieldName: 'orderNum',
      label: '排序',
      componentProps: {
        placeholder: '请输入排序',
        min: 0,
        max: 999,
      },
      rules: [{ required: true, message: '请输入排序' }],
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
      component: 'Switch',
      fieldName: 'isExt',
      label: '是否外部链接',
      componentProps: {
        trueValue: true,
        falseValue: false,
        defaultValue: false,
      },
    },
    {
      component: 'Switch',
      fieldName: 'hidden',
      label: '是否隐藏',
      componentProps: {
        trueValue: true,
        falseValue: false,
        defaultValue: false,
      },
    },
    {
      component: 'Switch',
      fieldName: 'keepAlive',
      label: '是否缓存',
      componentProps: {
        trueValue: true,
        falseValue: false,
        defaultValue: false,
      },
    },
    {
      component: 'Switch',
      fieldName: 'showBreadcrumb',
      label: '是否显示面包屑',
      componentProps: {
        trueValue: true,
        falseValue: false,
        defaultValue: true,
      },
    },
    {
      component: 'Input',
      fieldName: 'permission',
      label: '权限标识',
      componentProps: {
        placeholder: '请输入权限标识',
        maxlength: 100,
      },
    },
  ],
});

// 获取菜单列表
const getList = async () => {
  loading.value = true;
  try {
    const params = {
      ...searchForm.value,
      page: pagination.value.current,
      pageSize: pagination.value.pageSize,
    };
    const res = await getMenuListApi(params);
    tableData.value = res.data || [];
    pagination.value.total = res.total || 0;
  } catch (error) {
    console.error('获取菜单列表失败', error);
  } finally {
    loading.value = false;
  }
};

// 获取所有菜单（树形结构）
const getAllMenus = async () => {
  try {
    const res = await getAllMenusApi();
    treeData.value = res.data || [];
  } catch (error) {
    console.error('获取菜单树失败', error);
  }
};

// 打开新增抽屉
const handleAdd = () => {
  formApi.setValues({});
  drawer.title = '新增菜单';
  open();
};

// 打开编辑抽屉
const handleEdit = (row: any) => {
  formApi.setValues(row);
  drawer.title = '编辑菜单';
  open();
};

// 删除菜单
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该菜单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    await deleteMenuApi([row.id]);
    ElMessage.success('删除成功');
    getList();
    getAllMenus();
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
    ElMessage.warning('请选择要删除的菜单');
    return;
  }
  try {
    await ElMessageBox.confirm('确定要删除选中的菜单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    const ids = selectedRows.value.map((row) => row.id);
    await deleteMenuApi(ids);
    ElMessage.success('批量删除成功');
    selectedRows.value = [];
    getList();
    getAllMenus();
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
    title: '',
    status: undefined,
  };
  getList();
};

// 获取菜单类型文本
const getMenuTypeText = (type: number) => {
  const typeMap = {
    0: '目录',
    1: '菜单',
    2: '按钮',
  };
  return typeMap[type as keyof typeof typeMap] || '未知';
};

// 表格列配置
const columns = [
  {
    title: '菜单名称',
    dataIndex: 'title',
    key: 'title',
    width: 200,
  },
  {
    title: '菜单类型',
    dataIndex: 'type',
    key: 'type',
    width: 100,
    render: (type: number) => {
      return getMenuTypeText(type);
    },
  },
  {
    title: '路由路径',
    dataIndex: 'path',
    key: 'path',
    width: 200,
  },
  {
    title: '组件路径',
    dataIndex: 'component',
    key: 'component',
    ellipsis: true,
    width: 300,
  },
  {
    title: '图标',
    dataIndex: 'icon',
    key: 'icon',
    width: 100,
    render: (icon: string) => {
      return icon ? h('i', { class: icon }, '') : '-';
    },
  },
  {
    title: '排序',
    dataIndex: 'orderNum',
    key: 'orderNum',
    width: 80,
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100,
    render: (status: boolean) => {
      return h(
        'span',
        { class: status ? 'text-green-500' : 'text-red-500' },
        status ? '启用' : '禁用',
      );
    },
  },
  {
    title: '权限标识',
    dataIndex: 'permission',
    key: 'permission',
    ellipsis: true,
    width: 200,
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
        <h1 class="text-xl font-bold">菜单管理</h1>
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
            v-model="searchForm.title"
            placeholder="请输入菜单名称"
            clearable
            @keyup.enter="handleSearch"
            class="w-64"
          >
            <template #prefix>
              <i class="lucide:menu"></i>
            </template>
          </el-input>
        </div>
        <div class="w-full md:w-auto">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            class="w-48"
          >
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
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
    <Form />
  </drawer>
</template>
