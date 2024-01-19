# recommendations/recommendations.py

from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
 BookCategory,
 BookRecommendation,
 RecommendationResponse,
)

import recommendations_pb2_grpc

books_by_category = {
 BookCategory.MYSTERY: [
 BookRecommendation(id=1, title="Мальтийский сокол"),
 BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
 BookRecommendation(id=3, title="Собака Баскервилей"),
 BookRecommendation(id=4, title="Автостопом по галактике"),
 BookRecommendation(id=5, title="Игра Эндера"),
 BookRecommendation(id=6, title="Девушка с татуировкой дракона"),
 BookRecommendation(id=7, title="Безмолвный пациент"),
 BookRecommendation(id=8, title="Женщина в белом"),
 BookRecommendation(id=9, title="Остров проклятых"),
 BookRecommendation(id=10, title="Молчание ягнят"),
 ],
 BookCategory.SCIENCE_FICTION: [
 BookRecommendation(id=11, title="Дюна"),
 BookRecommendation(id=12, title="451' по Фаренгейту"),
 BookRecommendation(id=13, title="Нейромант"),
 BookRecommendation(id=14, title="Улитка на склоне столетия"),
 BookRecommendation(id=15, title="Автостопом по галактике"),
 BookRecommendation(id=16, title="Проект 'Аве Мария'"),
 BookRecommendation(id=17, title="Видоизмененный углерод. Такеси Ковач"),
 BookRecommendation(id=18, title="Машина времени"),
 BookRecommendation(id=19, title="Роузуотер"),
 BookRecommendation(id=20, title="Дитя человеческое"),
 ],
 BookCategory.SELF_HELP: [
 BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
 BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
 BookRecommendation(id=23, title="Человек в поисках смысла"),
 BookRecommendation(id=24, title="Прочь из замкнутого круга"),
 BookRecommendation(id=25, title="Компас Эмоций"),
 BookRecommendation(id=26, title="К себе нежно"),
 BookRecommendation(id=27, title="Осколки детских травм"),
 BookRecommendation(id=28, title="Мечтать не вредно"),
 BookRecommendation(id=29, title="Как перестать беспокоиться и начать жить"),
 BookRecommendation(id=30, title="Исцели свою жизнь"),
 ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
 def Recommend(self, request, context):
   if request.category not in books_by_category:
     context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
   books_for_category = books_by_category[request.category]
   num_results = min(request.max_results, len(books_for_category))
   books_to_recommend = random.sample(books_for_category, num_results)
   return RecommendationResponse(recommendations=books_to_recommend)

def serve():
 server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
 RecommendationService(), server
 )
 server.add_insecure_port("[::]:50051")
 server.start()
 server.wait_for_termination()

if __name__ == "__main__":
 serve()
