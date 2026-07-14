def test_register_success(client):
    response = client.post(
        "/register",
        json={"name": "New User", "email": "new@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_duplicate_email(client, test_user):
    # test_user 在夹具中已经被创建了，邮箱是 test@example.com
    response = client.post(
        "/register",
        json={"name": "Duplicate", "email": test_user.email, "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "该邮箱已被注册"

def test_login_success(client, test_user):
    response = client.post(
        "/login",
        json={"email": test_user.email, "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client, test_user):
    response = client.post(
        "/login",
        json={"email": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_create_todo(client, auth_headers):
    response = client.post(
        "/todos",
        headers=auth_headers,
        json={"title": "Learn Pytest", "description": "Write some test cases", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn Pytest"
    assert "id" in data

def test_get_todos_empty(client, auth_headers):
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_todos_with_data_and_filters(client, auth_headers):
    # 创建几个 todo
    client.post("/todos", headers=auth_headers, json={"title": "Todo 1", "completed": False})
    client.post("/todos", headers=auth_headers, json={"title": "Todo 2", "completed": True})
    
    # 1. 查询全部
    res_all = client.get("/todos", headers=auth_headers)
    assert len(res_all.json()) == 2
    
    # 2. 查询已完成
    res_completed = client.get("/todos?completed=true", headers=auth_headers)
    assert len(res_completed.json()) == 1
    assert res_completed.json()[0]["title"] == "Todo 2"
    
    # 3. 关键字搜索
    res_search = client.get("/todos?search=1", headers=auth_headers)
    assert len(res_search.json()) == 1
    assert res_search.json()[0]["title"] == "Todo 1"

def test_update_todo(client, auth_headers):
    # 创建
    create_res = client.post("/todos", headers=auth_headers, json={"title": "Initial Title"})
    todo_id = create_res.json()["id"]
    
    # 更新
    update_res = client.put(
        f"/todos/{todo_id}",
        headers=auth_headers,
        json={"title": "Updated Title", "completed": True}
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated Title"
    assert update_res.json()["completed"] is True

def test_delete_todo(client, auth_headers):
    create_res = client.post("/todos", headers=auth_headers, json={"title": "To be deleted"})
    todo_id = create_res.json()["id"]
    
    # 删除
    del_res = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert del_res.status_code == 204
    
    # 删除后查不到了
    get_res = client.get("/todos", headers=auth_headers)
    assert len(get_res.json()) == 0

def test_unauthorized_access(client):
    # 不带 header 访问受保护接口
    response = client.get("/todos")
    assert response.status_code == 401
