# Security filter chain

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http, OAuth2SuccessHandler oauthHandler) throws Exception {
        return http
                .cors(Customizer.withDefaults())
                .csrf(csrf -> csrf.disable())
                .headers(headers -> headers.frameOptions(frame -> frame.disable()))
                .authorizeHttpRequests(auth -> {
                    auth.requestMatchers("/", "/h2-console/**").permitAll();
                    auth.anyRequest().authenticated();
                })
                .oauth2Login(oauth -> {
                    oauth.successHandler(oauthHandler);
                    // oauth.defaultSuccessUrl("/", true);
                })
                .formLogin(form -> form.disable())
                .build();
    }
}
```