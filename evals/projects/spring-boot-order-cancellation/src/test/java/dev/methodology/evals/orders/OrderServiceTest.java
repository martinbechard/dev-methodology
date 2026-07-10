package dev.methodology.evals.orders;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class OrderServiceTest {
    @Test
    void returnsAnExistingOrder() {
        OrderRepository repository = new StubOrderRepository(new OrderView(1, OrderStatus.PENDING));
        OrderService service = new OrderService(repository);

        assertThat(service.get(1)).isEqualTo(new OrderView(1, OrderStatus.PENDING));
    }

    @Test
    void rejectsAMissingOrder() {
        OrderRepository repository = new StubOrderRepository(null);
        OrderService service = new OrderService(repository);

        assertThatThrownBy(() -> service.get(99)).isInstanceOf(OrderNotFoundException.class);
    }

    private static final class StubOrderRepository extends OrderRepository {
        private final OrderView order;

        private StubOrderRepository(OrderView order) {
            super(null);
            this.order = order;
        }

        @Override
        public java.util.Optional<OrderView> findById(long id) {
            return java.util.Optional.ofNullable(order);
        }
    }
}
