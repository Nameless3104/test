package day06.utils;

import day06.po.User;

import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class BaseDao {

    private static String aDriver;
    private static String aUrl;
    private static String aUser;
    private static String aPassword;

    static {
        init();
    }

    private static void init() {
        // 1.创建Properties对象
        Properties ps = new Properties();
        // 2.拿到文件路径
        String path = "db.properties";
        // 3.通过输入流读取db.properties
        InputStream is = BaseDao.class.getClassLoader().getResourceAsStream(path);
        // 4.把值加载到ps
        try {
            ps.load(is);
        } catch (IOException e) {
            e.printStackTrace();
        }
        aDriver = ps.getProperty("db.Driver");
        aUrl = ps.getProperty("db.url");
        aUser = ps.getProperty("db.user");
        aPassword = ps.getProperty("db.password");
    }

    public static Connection getConnection() {
        Connection conn = null;
        try {
            Class.forName(aDriver);
            conn = DriverManager.getConnection(aUrl,aUser, aPassword);
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeAll(Connection conn, Statement stmt, ResultSet rs) {
        try {
            if (rs != null) rs.close();
            if (stmt != null) stmt.close();
            if (conn != null) conn.close();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }
    public static void closeAll(Connection conn, Statement stmt) {
        try {
            if (stmt != null) stmt.close();
            if (conn != null) conn.close();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }

    /**
     * 封装前面addUser、deleteUser等DML操作
     * @param aSql 一个sql语句
     * @param objs 任意数量的Object对象，填入sql语句相应的?
     * @return
     */
    public static int updateManipulate(String aSql, Object... objs){
        int num = 0;
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(aSql);
            for (int i=0; i < objs.length; i++){
                pstmt.setObject(i+1, objs[i]);
            }
            num = pstmt.executeUpdate();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt);
        }
        return num;
    }

    public static List<User> queryManipulate(String aSql, Object... objs){

        List<User> list = new ArrayList<User>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(aSql);
            for (int i = 0; i < objs.length; i++) {
                pstmt.setObject(i+1, objs[i]);
            }
            rs = pstmt.executeQuery();
            while (rs.next()){
                User user = new User();
                user.setaId(rs.getInt(1));
                user.setaName(rs.getString(2));
                user.setaPassword(rs.getString(3));
                list.add(user);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt, rs);
        }
        return list;

    }

    public static List<User> queryManipulate(String aSql){

        List<User> list = new ArrayList<User>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(aSql);
            rs = pstmt.executeQuery();
            while (rs.next()){
                User user = new User();
                user.setaId(rs.getInt(1));
                user.setaName(rs.getString(2));
                user.setaPassword(rs.getString(3));
                list.add(user);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt, rs);
        }
        return list;

    }


    public static void main(String[] args) {
        System.out.println(getConnection());
    }

}
