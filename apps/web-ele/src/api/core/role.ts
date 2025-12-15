import { requestClient } from '#/api/request';

/**
 * 获取角色列表
 */
export async function getRoleListApi(params?: any) {
  return requestClient.get('/system/role/list', { params });
}

/**
 * 创建角色
 */
export async function createRoleApi(data: any) {
  return requestClient.post('/system/role', data);
}

/**
 * 更新角色
 */
export async function updateRoleApi(id: number, data: any) {
  return requestClient.put(`/system/role/${id}`, data);
}

/**
 * 删除角色
 */
export async function deleteRoleApi(ids: number[]) {
  return requestClient.delete('/system/role', { data: { ids } });
}

/**
 * 更新角色状态
 */
export async function updateRoleStatusApi(ids: number[], status: boolean) {
  return requestClient.put('/system/role/status', { ids, status });
}

/**
 * 获取角色权限
 */
export async function getRolePermissionsApi(roleId: number) {
  return requestClient.get(`/system/role/${roleId}/permissions`);
}

/**
 * 更新角色权限
 */
export async function updateRolePermissionsApi(
  roleId: number,
  permissions: number[],
) {
  return requestClient.put(`/system/role/${roleId}/permissions`, {
    permissions,
  });
}
