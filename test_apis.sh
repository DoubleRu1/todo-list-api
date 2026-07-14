#!/bin/bash
echo "=== 1. 注册新用户 ==="
curl -s -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}' | jq
echo -e "\n"

echo "=== 2. 登录获取 Token ==="
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' | jq -r .access_token)
echo "获取到的 Token: $TOKEN"
echo -e "\n"

echo "=== 3. 创建一条 Todo ==="
TODO_ID=$(curl -s -X POST http://127.0.0.1:8000/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, Eggs, Bread", "completed": false}' | jq -r .id)
echo "创建的 Todo ID: $TODO_ID"
echo -e "\n"

echo "=== 4. 查询 Todo 列表 ==="
curl -s -X GET "http://127.0.0.1:8000/todos?limit=5" \
  -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n"

echo "=== 5. 更新刚才创建的 Todo (设为已完成) ==="
curl -s -X PUT http://127.0.0.1:8000/todos/$TODO_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, Eggs, Bread", "completed": true}' | jq
echo -e "\n"

echo "=== 6. 按标题过滤查询 ==="
curl -s -X GET "http://127.0.0.1:8000/todos?search=groceries" \
  -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n"

echo "=== 7. 删除刚才创建的 Todo ==="
curl -s -w "%{http_code}" -X DELETE http://127.0.0.1:8000/todos/$TODO_ID \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n(期望输出 HTTP 状态码 204)"
