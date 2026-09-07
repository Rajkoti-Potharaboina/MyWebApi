using System.Text.Json;
using Newtonsoft.Json;

public static class Program1
{
    public static void MapVulnerableEndpoints(WebApplication app)
    {
        // 4. Insecure Deserialization Endpoint (Vulnerable - APP0004)
        app.MapPost("/api/user/deserialize-vulnerable", (string input) =>
        {
            var settings = new JsonSerializerSettings
            {
                TypeNameHandling = TypeNameHandling.All
            };
            var data = JsonConvert.DeserializeObject(input, settings);
            return Results.Ok(data);
        });

        // 5. Weak Password Policy Endpoint (Vulnerable - APP0005)
        app.MapPost("/api/user/register-vulnerable", (UserRegistrationRequest request) =>
        {
            var password = request?.Password;
            bool isValid = !string.IsNullOrEmpty(password) && password.Length >= 4;

            if (!isValid)
            {
                return Results.BadRequest("Password is too short.");
            }

            return Results.Ok(new { Status = "Registration successful with a weak password policy." });
        });

        // 6. Broken Access Control Endpoint (Vulnerable - APP0006)
        app.MapGet("/api/admin/dashboard-vulnerable", () =>
        {
            return Results.Ok(new { SecretData = "Confidential administrative records exposed without authorization." });
        });
    }
}

// Helper model placed cleanly at the very bottom, outside the class
public record UserRegistrationRequest(string Username, string Password);