package day04.action;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

public class LoginServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        resp.setContentType("text/html;charset=" + encoding);
        req.setCharacterEncoding(encoding);
        PrintWriter out = resp.getWriter();

        String id = req.getParameter("id");
        if (!id.equals("")){
            int id2 = Integer.parseInt(id);
            out.println("id: "+id2 + "<br>" + "登录成功");
        } else {
            out.println("id为空");
        }
        req.getRequestDispatcher("/userQuery.do").forward(req,resp);
    }
}
