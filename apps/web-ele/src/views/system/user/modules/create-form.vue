<script lang="ts" setup>
import { ElMessage } from 'element-plus';

import { useVbenForm } from '#/adapter/form';
import { createUserApi, getDeptListApi, getRoleListApi } from '#/api';

// 定义事件
const emit = defineEmits<{
  (e: 'stateChange'): void;
  (e: 'close'): void;
}>();

// 表单配置
const [Form] = useVbenForm({
  layout: 'vertical',
  handleSubmit: async (values) => {
    try {
      await createUserApi(values);
      ElMessage.success('用户创建成功');
      emit('stateChange');
      emit('close');
    } catch (error) {
      ElMessage.error('用户创建失败');
      console.error(error);
    }
  },
  schema: [
    {
      component: 'Input',
      fieldName: 'username',
      label: '用户名',
      componentProps: {
        placeholder: '请输入用户名',
        maxlength: 50,
      },
      rules: [
        { required: true, message: '请输入用户名' },
        { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符' },
      ],
    },
    {
      component: 'Input',
      fieldName: 'nickname',
      label: '昵称',
      componentProps: {
        placeholder: '请输入昵称',
        maxlength: 50,
      },
    },
    {
      component: 'InputPassword',
      fieldName: 'password',
      label: '密码',
      componentProps: {
        placeholder: '请输入密码',
        maxlength: 20,
      },
      rules: [
        { required: true, message: '请输入密码' },
        { min: 6, max: 20, message: '密码长度在 6 到 20 个字符' },
      ],
    },
    {
      component: 'Input',
      fieldName: 'email',
      label: '邮箱',
      componentProps: {
        placeholder: '请输入邮箱',
        maxlength: 100,
      },
      rules: [{ type: 'email', message: '请输入正确的邮箱地址' }],
    },
    {
      component: 'Input',
      fieldName: 'phone',
      label: '手机号',
      componentProps: {
        placeholder: '请输入手机号',
        maxlength: 20,
      },
    },
    {
      component: 'ApiSelect',
      fieldName: 'deptId',
      label: '所属部门',
      componentProps: {
        api: getDeptListApi,
        afterFetch: (data: any[]) => {
          return data.map((item) => ({
            label: item.name,
            value: item.id,
          }));
        },
        placeholder: '请选择部门',
      },
    },
    {
      component: 'ApiSelect',
      fieldName: 'roleIds',
      label: '角色',
      componentProps: {
        api: getRoleListApi,
        afterFetch: (data: any[]) => {
          return data.map((item) => ({
            label: item.name,
            value: item.id,
          }));
        },
        multiple: true,
        placeholder: '请选择角色',
      },
      rules: [{ required: true, message: '请选择角色' }],
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
  ],
});
</script>

<template>
  <div class="p-4">
    <Form />
  </div>
</template>
