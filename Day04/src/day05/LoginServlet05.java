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

public class LoginServlet05 extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        resp.setContentType("text/html;charset=" + encoding);
        req.setCharacterEncoding(encoding);

//        1.获取jsp中的值
        String username = req.getParameter("username");
        String pwd = req.getParameter("pwd");

//        2.创建业务层代码
        UserService userService = new UserServiceImpl();

//        3.调用业务层代码
        User user = userService.login(username, pwd);

//        4.判断user是否有值
        if (null != user){
//            转发
            req.getRequestDispatcher("/userQueryDay05.do").forward(req,resp);
        } else {
//            重定向
            resp.sendRedirect("day05/login05.jsp");
        }

    }
}
