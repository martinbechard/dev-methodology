package dev.methodology.evals.orders;

import java.util.Optional;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

@Repository
public class OrderRepository {
    private final JdbcClient jdbcClient;

    public OrderRepository(JdbcClient jdbcClient) {
        this.jdbcClient = jdbcClient;
    }

    public Optional<OrderView> findById(long id) {
        return jdbcClient.sql("select id, status from customer_order where id = :id")
                .param("id", id)
                .query((row, ignored) -> new OrderView(
                        row.getLong("id"),
                        OrderStatus.valueOf(row.getString("status"))))
                .optional();
    }
}
