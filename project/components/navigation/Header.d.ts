import * as React from 'react';

export interface NavItem {
  label: string;
  href: string;
}

export interface HeaderProps {
  logoSrc?: string;
  navItems?: NavItem[];
  phone?: string;
  /** label of the currently active nav item */
  active?: string;
}

export function Header(props: HeaderProps): JSX.Element;
