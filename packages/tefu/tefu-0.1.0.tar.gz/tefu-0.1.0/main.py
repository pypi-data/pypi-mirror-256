a = int(input())
b = map(int, input().split())
msg = input()

print(
    f"""
{sum([a, *b])}
{msg}
"""
)
