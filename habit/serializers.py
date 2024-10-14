from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычек текущего пользователя"""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        request = self.context.get("request")  # Получаем текущий запрос
        habit = Habit.objects.create(
            owner=request.user, **validated_data
        )  # Устанавливаем пользователя как владельца
        return habit

    def validate(self, data):
        # Проверка на одновременное наличие вознаграждения и связанной привычки
        if data.get("reward") and data.get("conn_habit"):
            raise serializers.ValidationError(
                "Нельзя указывать и вознаграждение, и связанную привычку одновременно. Выберите одно."
            )

        # Проверка времени выполнения (максимум 120 секунд)
        time_to_complete = data.get("time_to_complete")
        if time_to_complete and time_to_complete > 120:
            raise serializers.ValidationError(
                "Время на выполнение привычки не должно превышать 120 секунд."
            )

        # Проверка, что в связанные привычки попадают только приятные привычки
        if data.get("conn_habit") and not data.get("conn_habit").sign:
            raise serializers.ValidationError(
                "Связанной может быть только приятная привычка."
            )

        # Проверка, что у приятной привычки нет вознаграждения или связанной привычки
        if data.get("sign"):  # Признак приятной привычки
            if data.get("reward") or data.get("conn_habit"):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть ни вознаграждения, ни связанной привычки."
                )

        # Проверка периодичности (не реже 1 раза в 7 дней)
        periodicity = data.get("periodicity")
        if periodicity is not None:
            if periodicity < 1 or periodicity > 7:
                raise serializers.ValidationError(
                    "Периодичность должна быть в пределах от 1 до 7 дней."
                )
        else:
            raise serializers.ValidationError(
                "Поле периодичности не может быть пустым."
            )

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек"""

    class Meta:
        model = Habit
        fields = "__all__"
