import * as React from 'react';

export interface FooterProps {
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
}

export function Footer(props: FooterProps): JSX.Element;
