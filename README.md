![Python-WebSite-Screenshot](https://socialify.git.ci/zkeq/Python-WebSite-Screenshot/image?description=1&font=Bitter&forks=1&language=1&name=1&owner=1&pattern=Plus&stargazers=1&theme=Dark)

### 本项目是由 `Python` 写成的网站截图工具。

> 支持中文网站截图，该功能由 [valetzx](https://github.com/zkeq/Python-WebSite-Screenshot/pull/1) 开发。

#### 使用方法

1. 在 list.json 中填入你的网站列表。
2. 在 Github 生成一个 TOKEN 并且赋予 repo 权限
3. 在 环境变量中填入 `MY_GIT_TOKEN`，该环境变量用于将截好的图再次放回 GitHub。

#### 参数说明

| 参数 | 说明 |
| --- | --- |
| `url` | 网站网址 |
| `timeout` | sele 模块中等待时间，加载出网站后会停止（秒） |
| `real_time_out` | 强制等待时间，在上述 timeout 后休眠时间（秒） |
| `width` | 截图宽度 |
| `height` | 截图高度 |
| `daydel` | 截图的保存时间（天） |