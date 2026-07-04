import * as React from 'react';

export interface BadgeProps {
  children: React.ReactNode;
  tone?: 'navy' | 'ice' | 'red' | 'outline';
  style?: React.CSSProperties;
}

export function Badge(props: BadgeProps): JSX.Element;
