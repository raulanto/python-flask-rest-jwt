from app.models import Ship, User, db


class Database:
    def all_ships(self):
        return Ship.query.all()

    def all_users(self):
        return User.query.all()

    def get_ship(self, id):
        return Ship.query.get(id)

    def get_user(self, id):
        return User.query.get(id)

    def get_user_by_name(self, username):
        return User.query.filter_by(username=username).first()

    def add_ship(self, ship):
        db.session.add(ship)
        db.session.commit()
        return ship

    def add_user(self, user):
        if self.get_user_by_name(user.username):
            return None  # Evitar duplicados
        db.session.add(user)
        db.session.commit()
        return user

    def update_ship(self, ship):
        db.session.commit()
        return True

    def update_user(self, user):
        db.session.commit()
        return True

    def delete_ship(self, id):
        ship = self.get_ship(id)
        if ship:
            db.session.delete(ship)
            db.session.commit()
            return True
        return False

    def delete_user(self, id):
        user = self.get_user(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False