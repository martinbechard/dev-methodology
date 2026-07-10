create table customer_order (
    id bigint primary key,
    status varchar(32) not null check (status in ('PENDING', 'FULFILLED', 'CANCELLED'))
);
