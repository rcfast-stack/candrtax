import * as React from 'react';

export interface ContactCardProps {
  address?: string;
  areaNote?: string;
  phone?: string;
  email?: string;
  website?: string;
}

export function ContactCard(props: ContactCardProps): JSX.Element;
