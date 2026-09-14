var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseExceptionHandler(handler => handler.Run(async context =>
{
    context.Response.StatusCode = StatusCodes.Status500InternalServerError;
    await context.Response.WriteAsJsonAsync(new ApiResponse<object>(
        false,
        null,
        new ApiError("INTERNAL_ERROR", "خطای غیرمنتظره‌ای رخ داد."),
        context.TraceIdentifier));
}));

var users = new[] { new UserDto(1, "Mohammad Amin") };

app.MapGet("/api/users/{id:int}", (int id, HttpContext context) =>
{
    var user = users.FirstOrDefault(item => item.Id == id);
    return user is null
        ? Results.NotFound(new ApiResponse<UserDto>(
            false, null, new ApiError("USER_NOT_FOUND", "کاربر پیدا نشد."),
            context.TraceIdentifier))
        : Results.Ok(new ApiResponse<UserDto>(
            true, user, null, context.TraceIdentifier));
});

app.Run();

public sealed record UserDto(int Id, string Name);
public sealed record ApiError(
    string Code,
    string Message,
    IReadOnlyDictionary<string, string[]>? Details = null);
public sealed record ApiResponse<T>(
    bool Success,
    T? Data,
    ApiError? Error,
    string TraceId);

