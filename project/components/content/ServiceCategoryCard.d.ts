import * as React from 'react';

export interface ServiceCategoryCardProps {
  /** Lucide icon name */
  icon?: string;
  title: string;
  /** small italic footnote, e.g. mobile-service travel fee disclaimer */
  note?: string;
  items?: string[];
}

export function ServiceCategoryCard(props: ServiceCategoryCardProps): JSX.Element;
