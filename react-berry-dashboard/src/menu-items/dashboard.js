// assets
import { IconDashboard, IconDeviceAnalytics, IconFileUpload } from '@tabler/icons';

// constant
const icons = {
    IconDashboard: IconDashboard,
    IconFileUpload: IconFileUpload,
    IconDeviceAnalytics
};

//-----------------------|| DASHBOARD MENU ITEMS ||-----------------------//

export const dashboard = {
    id: 'dashboard',
    title: 'Dashboard',
    type: 'group',
    children: [
        {
            id: 'default',
            title: 'Dashboard',
            type: 'item',
            url: '/dashboard/default',
            icon: icons['IconDashboard'],
            breadcrumbs: false
        },
        {
            id: 'sample-page',
            title: 'Upload',
            type: 'item',
            url: '/sample-page',
            icon: icons['IconFileUpload'],
            breadcrumbs: false
        }
    ]
};
