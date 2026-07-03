
# OIDC snippets


```java
@Component
@Slf4j
public class OAuth2SuccessHandler extends SavedRequestAwareAuthenticationSuccessHandler {

    AppUserRepo userRepository; // app secific user repo

    public OAuth2SuccessHandler(AppUserRepo userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
            HttpServletResponse response,
            Authentication authentication) throws IOException, ServletException {

                
        log.info("OAuth2SuccessHandler called");
        OidcUser oauthUser = (OidcUser) authentication.getPrincipal();
        Optional<AppUser> user = userRepository.findByEmail(oauthUser.getEmail());

        if (user.isEmpty()) {
            AppUser newUser = AppUser.builder() // app specific user
                    .email(oauthUser.getEmail())
                    .firstName(oauthUser.getGivenName())
                    .lastName(oauthUser.getFamilyName())
                    .fullName(oauthUser.getFullName())
                    .build();

            AppUser saved = userRepository.save(newUser);
            log.info("Saved user id={}", saved.getEmail());
        } else {
            log.info("User exists: {}", user.isPresent());
        }
        super.onAuthenticationSuccess(request, response, authentication);
    }
}
```