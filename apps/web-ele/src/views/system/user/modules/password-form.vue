<script lang="ts" setup>
import { ElMessage } from 'element-plus';

import { useVbenForm } from '#/adapter/form';
import { updateUserApi } from '#/api';

// 获取父组件传递的数据
const props = defineProps<{
  rowData?: any;
  title?: string;
}>();

// 定义事件
const emit = defineEmits<{
  (e: 'stateChange'): void;
  (e: 'close'): void;
}>();

// 表单配置
const [Form, formApi] = useVbenForm({
  layout: 'vertical',
  handleSubmit: async (values) => {
    try {
      // 只传递密码字段
      await updateUserApi(props.rowData.id, { password: values.password });
      ElMessage.success('密码修改成功');
      emit('stateChange');
      emit('close');
    } catch (error) {
      ElMessage.error('密码修改失败');
      console.error(error);
    }
  },
  schema: [
    {
      component: 'InputPassword',
      fieldName: 'password',
      label: '新密码',
      componentProps: {
        placeholder: '请输入新密码',
        maxlength: 20,
      },
      rules: [
        { required: true, message: '请输入新密码' },
        { min: 6, max: 20, message: '密码长度在 6 到 20 个字符' },
      ],
    },
    {
      component: 'InputPassword',
      fieldName: 'confirmPassword',
      label: '确认密码',
      componentProps: {
        placeholder: '请再次输入新密码',
        maxlength: 20,
      },
      rules: [
        { required: true, message: '请确认密码' },
        {
          validator: (rule: any, value: string, callback: any) => {
            if (value === formApi.model.password) {
              callback();
            } else {
              callback(new Error('两次输入的密码不一致'));
            }
          },
          message: '两次输入的密码不一致',
        },
      ],
    },
  ],
});
</script>

<template>
  <div class="p-4">
    <Form />
  </div>
</template>
