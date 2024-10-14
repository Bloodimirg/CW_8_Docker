from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        reward = attrs.get('reward')
        conn_habit = attrs.get('conn_habit')
        time_to_complete = attrs.get('time_to_complete')
        periodicity = attrs.get('periodicity')
        is_pleasant = attrs.get('is_pleasant')

        # Проверка на одновременное заполнение reward и conn_habit
        if reward and conn_habit:
            raise serializers.ValidationError(
                "Не может быть заполнено одновременно поле вознаграждения и связанная привычка.")

        # Время выполнения должно быть не больше 120 секунд
        if time_to_complete > 120:
            raise serializers.ValidationError("Время на выполнение должно быть не больше 120 секунд.")

        # Связанная привычка может быть только приятной
        if conn_habit and not conn_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if is_pleasant and (reward or conn_habit):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        # Периодичность выполнения привычки не может быть менее 1 раз в 7 дней
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError("Периодичность выполнения привычки должна быть от 1 до 7 дней.")

        return attrs