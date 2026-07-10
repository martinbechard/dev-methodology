package dev.methodology.evals.orders;

import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderView get(long id) {
        return repository.findById(id).orElseThrow(() -> new OrderNotFoundException(id));
    }
}
