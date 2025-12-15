import type { UserInfo } from '@vben/types';

import { requestClient } from '#/api/request';

/**
 * 获取用户信息
 */
export async function getUserInfoApi() {
  return requestClient.get<UserInfo>('/user/info');
}

/**
 * 获取用户列表
 */
export async function getUserListApi(params?: any) {
  return requestClient.get('/system/user/list', { params });
}

/**
 * 创建用户
 */
export async function createUserApi(data: any) {
  return requestClient.post('/system/user', data);
}

/**
 * 更新用户
 */
export async function updateUserApi(id: number, data: any) {
  return requestClient.put(`/system/user/${id}`, data);
}

/**
 * 删除用户
 */
export async function deleteUserApi(ids: number[]) {
  return requestClient.delete('/system/user', { data: { ids } });
}

/**
 * 批量启用/禁用用户
 */
export async function updateUserStatusApi(ids: number[], status: boolean) {
  return requestClient.put('/system/user/status', { ids, status });
}
