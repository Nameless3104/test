package day04.po;

public class User {
    private String aName = "default name";
    private String aPassword = "default password";
    private int aId = 0;

    public User() {
    }

    public User(String aName, String aPassword) {
        this.aName = aName;
        this.aPassword = aPassword;
        this.aId = 0;
    }

    public User(String aName, String aPassword, int aId) {
        this.aName = aName;
        this.aPassword = aPassword;
        this.aId = aId;
    }

    public String getaName() {
        return aName;
    }

    public void setaName(String aName) {
        this.aName = aName;
    }

    public String getaPassword() {
        return aPassword;
    }

    public void setaPassword(String aPassword) {
        this.aPassword = aPassword;
    }

    public int getaId() {
        return aId;
    }

    public void setaId(int aId) {
        this.aId = aId;
    }

    @Override
    public String toString() {
        return "User{" +
                "aName='" + aName + '\'' +
                ", aPassword='" + aPassword + '\'' +
                ", aId=" + aId +
                '}';
    }
}
