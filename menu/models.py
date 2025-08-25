from sqlalchemy import Integer, ForeignKey, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    recipes: Mapped[list["Recipes"]] = relationship("Recipes", back_populates="category")


class Recipes(Base):
    __tablename__ = "recipes"

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    available_on_menu: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    author: Mapped["User"] = relationship("User", back_populates="recipes")
    category: Mapped["Category"] = relationship("Category", back_populates="recipes")
    ingredients: Mapped[list["Recipe_Ingredient"]] = relationship("Recipe_Ingredient", back_populates="recipe")


class Ingredients(Base):
    __tablename__ = "ingredients"

    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    unit: Mapped[str] = mapped_column(String, nullable=False)

    recipes: Mapped[list["Recipe_Ingredient"]] = relationship("Recipe_Ingredient", back_populates="ingredient")


class Recipe_Ingredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.recipe_id"), nullable=False)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.ingredient_id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    recipe: Mapped["Recipes"] = relationship("Recipes", back_populates="ingredients")
    ingredient: Mapped["Ingredients"] = relationship("Ingredients", back_populates="recipes")
