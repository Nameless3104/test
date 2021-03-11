package day04.dao;

import day04.po.User;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import static day04.utils.BaseDao.*;

public class UserDaoImpl implements UserDao{

    @Override
    public List<User> queryAll(User aUser) {
        List list = new ArrayList<User>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            conn = getConnection();
            String sql = "SELECT * FROM tusers";
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            while (rs.next()){
                User user = new User();
                user.setaName(rs.getString(1));
                user.setaPassword(rs.getString(2));
                user.setaId(rs.getInt(3));
                list.add(user);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt, rs);
        }
        return list;
    }

    @Override
    public User queryAUser(User aUser) {
        User user = null;
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            conn = getConnection();
            String sql = "SELECT * FROM tusers WHERE aname = ? AND apassword = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setObject(1, aUser.getaName());
            pstmt.setObject(2, aUser.getaPassword());
            rs = pstmt.executeQuery();
            while (rs.next()){
                user = new User();
                user.setaName(rs.getString(1));
                user.setaPassword(rs.getString(2));
                user.setaId(rs.getInt(3));
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt, rs);
        }
        return user;
    }
}
