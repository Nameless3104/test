package day06.action;

import day06.po.User;
import day06.service.UserService;
import day06.service.UserServiceImpl;
import day06.utils.PageInfo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet("/query06.do")
public class QueryAction extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req,resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);


        int pageCurr = 1;
        PageInfo pageInfo = new PageInfo();
        pageInfo.setPageCurrent(pageCurr);

        UserService userService = new UserServiceImpl();
        List<User> list = userService.queryAllPage(pageInfo, null);
        int totalCount = userService.getTotalCount();
        pageInfo.setTotalCount(totalCount);
        int pageSize = pageInfo.getPageSize();
        int pageCount = (int) Math.ceil((double)totalCount / (double) pageSize);
        pageInfo.setPageCount(pageCount);

        req.setAttribute("list", list);
        req.setAttribute("pageInfo", pageInfo);
        req.getRequestDispatcher("/day06/UserList.jsp").forward(req, resp);
    }
}
