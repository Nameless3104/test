package day05;

import day04.po.User;
import day04.service.UserService;
import day04.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class UserQueryAction05 extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        resp.setContentType("text/html;charset=" + encoding);
        req.setCharacterEncoding(encoding);

//        1.创建对象
        UserService userService = new UserServiceImpl();

//        2.调用业务层代码
        List<User> list = userService.queryAll(null);

//        3.把list的值存在 HttpServletRequest作用域中
        req.setAttribute("userList", list);

//        4.必须通过转发的方式
        req.getRequestDispatcher("/day05/UserList05.jsp").forward(req, resp);
    }
}
