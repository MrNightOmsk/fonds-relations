"use client"

import React from 'react';
import { Button } from "@/components/ui/button"

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">Система анализа фондов</h1>
      
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4">О проекте</h2>
        <p className="text-gray-600 mb-4">
          Добро пожаловать в систему анализа фондов и их взаимосвязей. Этот инструмент помогает отслеживать и анализировать отношения между различными фондами, их активами и операциями.
        </p>
        <p className="text-gray-600">
          Используйте навигационное меню выше для доступа к основным функциям:
        </p>
        <ul className="list-disc list-inside mt-2 text-gray-600">
          <li>Просмотр и управление фондами</li>
          <li>Анализ связей между фондами</li>
          <li>Детальная аналитика и отчеты</li>
        </ul>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-blue-50 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-3">Фонды</h3>
          <p className="text-gray-600">Управляйте информацией о фондах, их активах и характеристиках</p>
        </div>
        <div className="bg-green-50 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-3">Связи</h3>
          <p className="text-gray-600">Исследуйте и анализируйте взаимосвязи между различными фондами</p>
        </div>
        <div className="bg-purple-50 rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-3">Аналитика</h3>
          <p className="text-gray-600">Получайте детальные отчеты и статистику по работе фондов</p>
        </div>
      </div>
    </div>
  );
}