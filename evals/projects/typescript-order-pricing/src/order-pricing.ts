export type OrderLine = Readonly<{
  quantity: number;
  unitPriceCents: number;
}>;

export type OrderQuote = Readonly<{
  subtotalCents: number;
  totalCents: number;
}>;

export function quoteOrder(lines: readonly OrderLine[]): OrderQuote {
  const subtotalCents = lines.reduce(
    (total, line) => total + line.quantity * line.unitPriceCents,
    0,
  );
  return { subtotalCents, totalCents: subtotalCents };
}
