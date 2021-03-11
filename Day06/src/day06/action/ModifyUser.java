package day06.action;

import day06.po.User;
import day06.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/modifyUser.do")
public class ModifyUser extends HttpServlet {


    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        int id = Integer.parseInt(req.getParameter("id"));

        String username = req.getParameter("username");
        String pwd = req.getParameter("pwd");

        User aUser = new User(username, pwd, id);

        int i = new UserServiceImpl().updateUser(aUser);

        if (i > 0){
            req.getRequestDispatcher("/query06.do").forward(req, resp);
        } else {
            resp.sendRedirect("/Day06_war_exploded/day06/login06.jsp"); // 重定向至登录页面
        }

    }
}