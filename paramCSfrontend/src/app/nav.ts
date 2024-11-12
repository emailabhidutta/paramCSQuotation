import { INavData } from '@coreui/angular';

export const navItems: INavData[] = [
  {
    name: 'Dashboard',
    url: '/dashboard',
    iconComponent: { name: 'cil-speedometer' }
  },
  {
    name: 'Create Quote',
    url: '/quotes/create',
    iconComponent: { name: 'cil-plus' }
  },
  {
    name: 'Quotes',
    url: '/quotes',
    iconComponent: { name: 'cil-description' },
    children: [
      {
        name: 'All Quotes',
        url: '/quotes/all'
      },
      {
        name: 'Accepted Quotes',
        url: '/quotes/accepted'
      },
      {
        name: 'Rejected Quotes',
        url: '/quotes/rejected'
      },
      {
        name: 'Cancelled Quotes',
        url: '/quotes/cancelled'
      }
    ]
  },
  {
    name: 'Masters',
    iconComponent: { name: 'cil-settings' },
    children: [
      {
        name: 'Users',
        url: '/master/users',
        iconComponent: { name: 'cil-user' }
      },
      {
        name: 'Roles',
        url: '/master/roles',
        iconComponent: { name: 'cil-people' }
      }
    ]
  }
];
