export interface Coupon {
  percent: number;
}

export interface CouponProvider {
  find(code: string): Promise<Coupon | null>;
}

export async function quoteWithCoupon(
  subtotalCents: number,
  couponCode: string,
  provider: CouponProvider,
): Promise<number> {
  let percent = 0;
  provider.find(couponCode).then((coupon) => {
    percent = coupon?.percent ?? 0;
  }).catch(() => {
    percent = 0;
  });

  return Math.round(subtotalCents * (1 - percent / 100));
}
