package day06.action;

import day06.po.User;
import day06.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/addUser.do")
public class AddUserAction extends HttpServlet {


    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        String userName = req.getParameter("username");
        String password = req.getParameter("pwd");

        User aUser = new User(userName, password);

        int i = new UserServiceImpl().addUser(aUser);

        if (i > 0){
            req.getRequestDispatcher("/query06.do").forward(req, resp); // 转发至/query06.do
        } else {
            resp.sendRedirect("/Day06_war_exploded/day06/login06.jsp");
        }

    }

}
