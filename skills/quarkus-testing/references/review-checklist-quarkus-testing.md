# Quarkus Testing Review Checklist

- Question: Is each test using the smallest plain JUnit, component, QuarkusTest, or integration boundary that proves its claim?
- Question: Are test annotations, profiles, CDI replacements, and resource mechanisms supported by the configured Quarkus line?
- Question: Do Dev Services, test resources, databases, and external-service replacements provide sufficient production fidelity and correct lifecycle behavior?
- Question: Are build-time configuration, runtime overrides, profiles, ports, clocks, identifiers, and mutable fixtures deterministic and isolated?
- Question: Do tests cover validation, authentication, authorization, translated failures, transaction outcomes, execution model, and side-effect timing where applicable?
- Question: Does the built-artifact test cover classpath, resources, launch behavior, and deployment configuration affected by the change?
- Question: Does native integration evidence exist when native delivery or compatibility-sensitive behavior changed?
- Question: Does reporting identify the test boundary, launch mode, profile, artifact form, database engine, services, and commands that actually ran?
