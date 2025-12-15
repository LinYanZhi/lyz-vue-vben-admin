<script lang="ts" setup>
import type { VbenFormProps } from '#/adapter/form';
import type {
  OnActionClickParams,
  VxeTableGridOptions,
} from '#/adapter/vxe-table';

import { Page } from '@vben/common-ui';

import { ElButton, ElMessage, ElSwitch } from 'element-plus';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { deleteUserApi, getUserListApi, updateUserStatusApi } from '#/api';

interface RowType {
  id: string;
  username: string;
  nickname: string;
  email: string;
  phone: string;
  roles: any[];
  deptName: string;
  status: boolean;
  created_at: string;
}

const formOptions: VbenFormProps = {
  // 默认展开
  collapsed: false,
  schema: [
    {
      component: 'Input',
      fieldName: 'username',
      label: '用户名',
    },
    {
      component: 'Input',
      fieldName: 'nickname',
      label: '用户昵称',
    },
    {
      component: 'Select',
      fieldName: 'status',
      label: '状态',
      componentProps: {
        options: [
          { label: '启用', value: true },
          { label: '禁用', value: false },
        ],
        placeholder: '请选择状态',
        clearable: true,
      },
    },
  ],
  // 控制表单是否显示折叠按钮
  showCollapseButton: true,
  // 是否在字段值改变时提交表单
  submitOnChange: true,
  // 按下回车时是否提交表单
  submitOnEnter: false,
};

const gridOptions: VxeTableGridOptions<RowType> = {
  checkboxConfig: {
    highlight: true,
    labelField: 'username',
  },
  columns: [
    { title: '序号', type: 'seq', width: 50 },
    { align: 'left', type: 'checkbox', width: 50 },
    { field: 'username', title: '账号' },
    { field: 'nickname', title: '昵称' },
    { field: 'email', title: '邮箱' },
    { field: 'phone', title: '手机号' },
    {
      field: 'roles',
      title: '角色',
      // formatter: ({ cellValue }) => cellValue.map((item: any) => item.name).join(', '),
    },
    { field: 'deptName', title: '部门' },
    {
      field: 'status',
      title: '状态',
      slots: { default: 'status' },
      width: 100,
    },
    { field: 'created_at', title: '创建时间', width: 180 },
    {
      field: 'action',
      slots: { default: 'action' },
      title: '操作',
      fixed: 'right',
      width: 150,
    },
  ],
  showOverflow: false,
  exportConfig: {},
  height: 'auto',
  keepSource: true,
  pagerConfig: {},
  proxyConfig: {
    ajax: {
      query: async ({ page }, formValues) => {
        return await getUserListApi({
          page: page.currentPage,
          pageSize: page.pageSize,
          ...formValues,
        });
      },
    },
  },
  toolbarConfig: {
    custom: true,
    export: true,
    refresh: true,
    resizable: true,
    search: true,
    zoom: true,
  },
};

// 导入或创建表单组件
// 注意：需要创建这些组件文件或调整路径
// import CreateFormModal from './modules/create-form.vue';
// import EditFormModal from './modules/edit-form.vue';
// import PasswordFormModal from './modules/password-form.vue';

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions,
  gridOptions,
});

// const [createModalEl, createModalApi] = useVbenModal({
//   connectedComponent: CreateFormModal,
//   destroyOnClose: true,
// });

// const [editModalEl, editModalApi] = useVbenModal({
//   connectedComponent: EditFormModal,
//   destroyOnClose: true,
// });

// const [passwordModalEl, passwordModalApi] = useVbenModal({
//   connectedComponent: PasswordFormModal,
//   destroyOnClose: true,
// });

// function edit(row: any) {
//   editModalApi.setData({ rowData: row, title: '编辑用户' });
//   editModalApi.open();
// }

function onActionClick(e: OnActionClickParams<any>) {
  switch (e.code) {
    case 'delete': {
      deleteUserApi([e.row.id])
        .then(() => {
          gridApi.reload();
          ElMessage.success('删除成功');
        })
        .catch(() => {
          ElMessage.error('删除失败');
        });
      break;
    }
    case 'edit': {
      // edit(e.row);
      break;
    }
  }
}

// function openNewData() {
//   createModalApi.setData({ title: '新增用户' });
//   createModalApi.open();
// }

// function openPassword(row: any) {
//   passwordModalApi.setData({ rowData: row, title: '修改密码' });
//   passwordModalApi.open();
// }

function handleStatusChange(row: any) {
  updateUserStatusApi([row.id], !row.status)
    .then(() => {
      gridApi.reload();
      ElMessage.success('状态更新成功');
    })
    .catch(() => {
      ElMessage.error('状态更新失败');
      // 恢复原状态
      row.status = !row.status;
    });
}
</script>

<template>
  <Page auto-content-height>
    <!-- 密码修改模态框 -->
    <!-- <passwordModalEl @state-change="handleSearch"></passwordModalEl> -->
    <!-- 新增用户模态框 -->
    <!-- <createModalEl @state-change="handleSearch"></createModalEl> -->
    <!-- 编辑用户模态框 -->
    <!-- <editModalEl @state-change="handleSearch"></editModalEl> -->
    <Grid>
      <template #action="{ row }">
        <!-- <ElButton type="primary" link @click="edit(row)" class="mr-2">编辑</ElButton> -->
        <ElButton
          type="danger"
          link
          @click="onActionClick({ code: 'delete', row })"
          class="mr-2"
        >
          删除
        </ElButton>
        <!-- <ElButton type="info" link @click="openPassword(row)">修改密码</ElButton> -->
      </template>
      <template #status="{ row }">
        <ElSwitch
          v-model="row.status"
          :active-value="true"
          :inactive-value="false"
          @change="handleStatusChange(row)"
        />
      </template>
      <template #toolbar-tools>
        <!-- <ElButton type="primary" @click="openNewData()">
          <template #icon>
            <i class="lucide:plus"></i>
          </template>
          新增
        </ElButton> -->
      </template>
    </Grid>
  </Page>
</template>
