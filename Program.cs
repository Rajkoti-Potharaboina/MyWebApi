using Microsoft.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

string connectionString = "Server=(localdb)\\mssqllocaldb;Database=DemoDb;Trusted_Connection=True;";

// 1. SQL Injection Endpoint (Vulnerable - APP0001)
app.MapGet("/api/user/search-vulnerable", (string username) =>
{
    // Vulnerable: Direct string concatenation
    string query = "SELECT * FROM Users WHERE Username = '" + username + "'";

    using (SqlConnection connection = new SqlConnection(connectionString))
    {
        SqlCommand command = new SqlCommand(query, connection);
        return Results.Ok(new
        {
            ExecutedQuery = query,
            Status = "Vulnerable query executed via string concatenation."
        });
    }
});

// 2. Cross-Site Scripting Endpoint (Vulnerable - APP0002)
app.MapGet("/api/user/xss", (string input) =>
{
    string html = "<h1>User Output: " + System.Net.WebUtility.HtmlEncode(input) + "</h1>";
    return Results.Content(html, "text/html");
});

// 3. Hardcoded Secret Endpoint (Vulnerable - APP0003)
app.MapGet("/api/user/config", () =>
{
    string secretKey = "SuperSecretKey12345!";
    return Results.Ok(new { ApiKey = secretKey });
});

app.Run();