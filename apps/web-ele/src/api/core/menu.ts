import type { RouteRecordStringComponent } from '@vben/types';

import { requestClient } from '#/api/request';

/**
 * 获取用户所有菜单
 */
export async function getAllMenusApi() {
  return requestClient.get<RouteRecordStringComponent[]>('/menu/all');
}

/**
 * 获取菜单列表
 */
export async function getMenuListApi(params?: any) {
  return requestClient.get('/system/menu/list', { params });
}

/**
 * 创建菜单
 */
export async function createMenuApi(data: any) {
  return requestClient.post('/system/menu', data);
}

/**
 * 更新菜单
 */
export async function updateMenuApi(id: number, data: any) {
  return requestClient.put(`/system/menu/${id}`, data);
}

/**
 * 删除菜单
 */
export async function deleteMenuApi(ids: number[]) {
  return requestClient.delete('/system/menu', { data: { ids } });
}
