<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 16:09
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<html>
<head>
    <title>Title</title>
</head>
<body>

<c:if test="${empty aUser || empty list}">
    <%
        response.sendRedirect("/Day06_war_exploded/day06/login06.jsp"); // 重定向至登录页面
    %>
</c:if>

<form>

    <table width="60%" border="1" cellpadding="0" cellspacing="0">
        <tr>
            <td>id</td>
            <td>用户名</td>
            <td>密码</td>
            <td>操作</td>
        </tr>

        <c:forEach var="li" items="${list}">
            <tr>
                <td>${li.aId}</td>
                <td>${li.aName}</td>
                <td>${li.aPassword}</td>
                <td>
                    <a href="${pageContext.request.contextPath}/day06/addUser.jsp">添加</a>
                    <a href="${pageContext.request.contextPath}/deleteUser.do?id=${li.aId}">删除</a>
                    <a href="${pageContext.request.contextPath}/findUserById.do?id=${li.aId}">修改</a>
                </td>
            </tr>
        </c:forEach>
    </table>

    <script>
        function ccc(){
            var i = document.getElementById("num").value;
            window.location.href = "${pageContext.request.contextPath}/userPageQuery.do?pageCurrent=" + i;
        }
    </script>

    <table>
        <tr>
            <td>
                总共${pageInfo.pageCount}页，当前第${pageInfo.pageCurrent}页，总共${pageInfo.totalCount}条数据 <br>
                跳转到第 <input type="number" value="1" id="num" style="width: 40px" min="1" max="${pageInfo.pageCount}"> 页 <input type="button" value="go" onclick="ccc()"> <br>
                <a href="${pageContext.request.contextPath}/userPageQuery.do?pageCurrent=1">首页</a>
                <c:if test="${pageInfo.pageCurrent > 1}">
                    <a href="${pageContext.request.contextPath}/userPageQuery.do?pageCurrent=${pageInfo.pageCurrent - 1}">上一页</a>
                </c:if>
                <c:if test="${pageInfo.pageCurrent <= 1}">
                    上一页
                </c:if>

                <c:if test="${pageInfo.pageCurrent < pageInfo.pageCount}">
                    <a href="${pageContext.request.contextPath}/userPageQuery.do?pageCurrent=${pageInfo.pageCurrent + 1}">下一页</a>
                </c:if>
                <c:if test="${pageInfo.pageCurrent >= pageInfo.pageCount}">
                    下一页
                </c:if>
                <a href="${pageContext.request.contextPath}/userPageQuery.do?pageCurrent=${pageInfo.pageCount}">末页</a>


            </td>
        </tr>
    </table>

</form>


</body>
</html>