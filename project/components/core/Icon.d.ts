import * as React from 'react';

export interface IconProps {
  /** Lucide icon name, kebab-case (e.g. "phone", "mail", "clock", "shield-check") */
  name: string;
  /** Pixel size, square. Default 20. */
  size?: number;
  /** CSS color. Default currentColor. */
  color?: string;
  /** SVG stroke width. Default 2. */
  strokeWidth?: number;
  style?: React.CSSProperties;
}

export function Icon(props: IconProps): JSX.Element;
