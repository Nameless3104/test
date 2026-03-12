# RAG Demo Frontend

基于 Vue 3 + Vite 的 RAG（检索增强生成）演示项目前端。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Composition API** - Vue 3 组合式 API

## 项目结构

```
frontend/
├── public/
│   └── favicon.ico          # 网站图标
├── src/
│   ├── assets/
│   │   └── style.css        # 全局样式
│   ├── components/
│   │   ├── ChatBox.vue      # 聊天输入框组件
│   │   ├── MessageList.vue  # 消息列表组件
│   │   ├── MessageItem.vue  # 单条消息组件
│   │   └── SourceCard.vue   # 来源卡片组件
│   ├── views/
│   │   └── Home.vue         # 主页面
│   ├── api/
│   │   └── chat.js          # API 调用封装
│   ├── App.vue              # 根组件
│   └── main.js              # 入口文件
├── index.html               # HTML 模板
├── package.json             # 项目配置
├── vite.config.js           # Vite 配置
└── README.md                # 项目说明
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 功能特性

- ✅ 现代化聊天界面
- ✅ 用户消息与 AI 消息区分显示
- ✅ 加载状态动画
- ✅ 错误处理
- ✅ 参考来源展示
- ✅ 响应式布局
- ✅ API 代理配置

## API 接口

前端通过代理连接后端 API：

- `POST /api/chat/` - 发送问题
- `GET /api/documents/` - 获取文档列表

## 注意事项

1. 确保后端服务运行在 `http://localhost:8000`
2. 开发环境下 API 请求会自动代理到后端
3. 生产环境需要配置 Nginx 或其他反向代理
