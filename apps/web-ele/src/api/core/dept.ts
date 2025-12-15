import { requestClient } from '#/api/request';

/**
 * 获取部门列表
 */
export async function getDeptListApi(params?: any) {
  return requestClient.get('/system/dept/list', { params });
}

/**
 * 创建部门
 */
export async function createDeptApi(data: any) {
  return requestClient.post('/system/dept', data);
}

/**
 * 更新部门
 */
export async function updateDeptApi(id: number, data: any) {
  return requestClient.put(`/system/dept/${id}`, data);
}

/**
 * 删除部门
 */
export async function deleteDeptApi(ids: number[]) {
  return requestClient.delete('/system/dept', { data: { ids } });
}
