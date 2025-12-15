import type { RouteRecordRaw } from 'vue-router';

import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'lucide:settings',
      order: 1000,
      title: $t('page.system.title'),
    },
    name: 'System',
    path: '/system',
    children: [
      {
        name: 'UserManagement',
        path: '/system/user',
        component: () => import('#/views/system/user/index.vue'),
        meta: {
          icon: 'lucide:users',
          title: $t('page.system.user'),
          permission: 'system:user:view',
        },
      },
      {
        name: 'RoleManagement',
        path: '/system/role',
        component: () => import('#/views/system/role/index.vue'),
        meta: {
          icon: 'lucide:user-check',
          title: $t('page.system.role'),
          permission: 'system:role:view',
        },
      },
      {
        name: 'MenuManagement',
        path: '/system/menu',
        component: () => import('#/views/system/menu/index.vue'),
        meta: {
          icon: 'lucide:menu',
          title: $t('page.system.menu'),
          permission: 'system:menu:view',
        },
      },
    ],
  },
];

export default routes;
