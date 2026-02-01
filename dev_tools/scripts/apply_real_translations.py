
import re

# Dictionary containing properly translated values for the keys that were previously filled with English
TRANSLATION_TWEAKS = {
    'hi': {
        'doc': 'तालाब में कुल दिन (DOC)', 'feed_consumed': 'कुल खपत (किलोग्राम)', 'predict_size': 'आकार और गुणवत्ता का अनुमान',
        'digital_logbook': 'डिजिटल लॉगबुक', 'secure_history': 'अपना डेटा सुरक्षित रखें', 'th_date': 'तारीख', 'th_notes': 'नोट्स',
        'add_log': '➕ नया लॉग जोड़ें', 'sust_tracker': 'स्थिरता ट्रैकर', 'eco_eff': 'इको-दक्षता मापें',
        'harvest_weight': 'कुल फसल वजन (किलोग्राम)', 'water_usage': 'जल उपयोग (घन मीटर)', 'gen_report': 'रिपोर्ट बनाएं',
        'export_compliance': 'निर्यात अनुपालन', 'intl_markets': 'अं.रा. बाजारों के लिए जाँच', 'target_region': 'लक्ष्य क्षेत्र',
        'avg_weight': 'औसत वजन (ग्राम)', 'check_eligibility': 'पात्रता की जाँच', 'visual_scan': 'AI विज़न स्कैन',
        'diagnose_visually': 'दृश्यक बीमारी निदान', 'upload_photo': 'फोटो अपलोड करें', 'vision_engine': 'त्वचा/गलफड़ों की जाँच',
        'start_scan': 'स्कैन शुरू करें', 'access_dash': 'डैशबोर्ड एक्सेस', 'phone_email': 'फ़ोन/ईमेल', 'get_otp': 'OTP प्राप्त करें',
        'sys_settings': 'सिस्टम सेटिंग्स', 'configure_otp': 'OTP कॉन्फ़िगर करें', 'demo_mode': 'डेमो मोड',
        'email_gateway': 'ईमेल गेटवे', 'sms_gateway': 'SMS गेटवे', 'save_config': 'सेव करें', 'back_home': 'वापस जाएं',
        'market_global_title': 'वैश्विक बाज़ार', 'market_global_desc': 'अंतर्राष्ट्रीय आपूर्तिकर्ताओं से ऑर्डर करें',
        'filter_country': 'देश फ़िल्टर', 'filter_species': 'प्रजाति फ़िल्टर', 'btn_order': 'ऑर्डर करें',
    },
    'es': {
        'doc': 'Días Totales (DOC)', 'feed_consumed': 'Consumo Total (kg)', 'predict_size': 'Predecir Tamaño',
        'digital_logbook': 'Cuaderno Digital', 'secure_history': 'Historial Seguro', 'th_date': 'Fecha', 'th_notes': 'Notas',
        'add_log': '➕ Agregar Registro', 'sust_tracker': 'Rastreador de Sostenibilidad', 'eco_eff': 'Eficiencia Ecológica',
        'harvest_weight': 'Peso Cosechado (kg)', 'water_usage': 'Uso de Agua (m3)', 'gen_report': 'Generar Reporte',
        'export_compliance': 'Cumplimiento Exportación', 'intl_markets': 'Verificar Mercados', 'target_region': 'Región Objetivo',
        'avg_weight': 'Peso Promedio (g)', 'check_eligibility': 'Verificar Elegibilidad', 'visual_scan': 'Escaneo Visual AI',
        'diagnose_visually': 'Diagnóstico Visual', 'upload_photo': 'Subir Foto', 'vision_engine': 'Análisis de piel/branquias',
        'start_scan': 'Iniciar Escaneo', 'access_dash': 'Acceder al Panel', 'phone_email': 'Teléfono/Email', 'get_otp': 'Obtener OTP',
        'sys_settings': 'Configuración del Sistema', 'configure_otp': 'Configurar OTP', 'demo_mode': 'Modo Demo',
        'email_gateway': 'Puerta de Enlace Email', 'sms_gateway': 'Puerta de Enlace SMS', 'save_config': 'Guardar', 'back_home': 'Volver',
        'market_global_title': 'Mercado Global', 'market_global_desc': 'Explorar proveedores internacionales',
        'filter_country': 'Filtrar por País', 'filter_species': 'Filtrar por Especie', 'btn_order': 'Ordenar',
        'order_msg': 'Pedido de {qty} toneladas de {species} desde {country}.', 'order_success': 'Pedido Exitoso',
        'status_waiting': 'ESPERANDO...', 'status_safe': 'ESTADO SEGURO',
    },
    'zh': {
        'doc': '养殖天数 (DOC)', 'feed_consumed': '总饲料消耗 (kg)', 'predict_size': '预测规格与质量',
        'digital_logbook': '数字日志', 'secure_history': '安全存储历史记录', 'th_date': '日期', 'th_notes': '备注',
        'add_log': '➕ 添加日志', 'sust_tracker': '可持续性追踪', 'eco_eff': '测量生态效率',
        'harvest_weight': '总收获重量 (kg)', 'water_usage': '总用水量 (立方米)', 'gen_report': '生成报告',
        'export_compliance': '出口合规性', 'intl_markets': '验证国际市场', 'target_region': '目标区域',
        'avg_weight': '当前平均重量 (g)', 'check_eligibility': '检查资格', 'visual_scan': 'AI 视觉扫描',
        'diagnose_visually': '视觉诊断疾病', 'upload_photo': '上传照片', 'vision_engine': '检测皮肤和鳃部',
        'start_scan': '开始扫描', 'access_dash': '访问仪表板', 'phone_email': '电话或邮箱', 'get_otp': '获取验证码',
        'sys_settings': '系统设置', 'configure_otp': '配置验证码', 'demo_mode': '演示模式',
        'email_gateway': '邮件网关', 'sms_gateway': '短信网关', 'save_config': '保存配置', 'back_home': '返回首页',
        'market_global_title': '全球市场', 'market_global_desc': '浏览国际供应商',
        'filter_country': '按国家筛选', 'filter_species': '按品种筛选', 'btn_order': '下单',
        'order_msg': '已订购 {country} 的 {species} {qty} 吨。', 'order_success': '下单成功',
    },
    'ar': {
        'doc': 'إجمالي الأيام (DOC)', 'feed_consumed': 'إجمالي العلف (كجم)', 'predict_size': 'توقع الحجم',
        'digital_logbook': 'السجل الرقمي', 'secure_history': 'تاريخ آمن', 'th_date': 'تاريخ', 'th_notes': 'ملاحظات',
        'add_log': '➕ إضافة سجل', 'sust_tracker': 'تتبع الاستدامة', 'eco_eff': 'كفاءة بيئية',
        'harvest_weight': 'وزن الحصاد (كجم)', 'water_usage': 'استخدام المياه (م3)', 'gen_report': 'إنشاء تقرير',
        'export_compliance': 'امتثال التصدير', 'intl_markets': 'التحقق من الأسواق', 'target_region': 'المنطقة المستهدفة',
        'avg_weight': 'متوسط الوزن (غ)', 'check_eligibility': 'تحقق من الأهلية', 'visual_scan': 'مسح بصري AI',
        'diagnose_visually': 'تشخيص بصري', 'upload_photo': 'رفع صورة', 'vision_engine': 'فحص الجلد والخياشيم',
        'start_scan': 'بدء المسح', 'access_dash': 'الدخول للوحة التحكم', 'phone_email': 'هاتف/بريد', 'get_otp': 'رمز التحقق',
        'sys_settings': 'إعدادات النظام', 'configure_otp': 'تكوين الرمز', 'demo_mode': 'وضع تجريبي',
        'email_gateway': 'بوابة البريد', 'sms_gateway': 'بوابة الرسائل', 'save_config': 'حفظ', 'back_home': 'عودة',
        'market_global_title': 'السوق العالمي', 'market_global_desc': 'تصفح الموردين الدوليين',
        'filter_country': 'تصفية حسب البلد', 'filter_species': 'تصفية حسب النوع', 'btn_order': 'طلب',
    },
    'fr': {
        'doc': 'Jours Totaux (DOC)', 'feed_consumed': 'Aliment Consommé (kg)', 'predict_size': 'Prédire Taille',
        'digital_logbook': 'Journal Numérique', 'secure_history': 'Historique Sécurisé', 'th_date': 'Date', 'th_notes': 'Notes',
        'add_log': '➕ Ajouter Entrée', 'sust_tracker': 'Suivi Durabilité', 'eco_eff': 'Efficacité Éco',
        'harvest_weight': 'Poids Récolté (kg)', 'water_usage': 'Eau Utilisée (m3)', 'gen_report': 'Générer Rapport',
        'export_compliance': 'Conformité Export', 'intl_markets': 'Vérifier Marchés', 'target_region': 'Région Cible',
        'avg_weight': 'Poids Moyen (g)', 'check_eligibility': 'Vérifier Éligibilité', 'visual_scan': 'Scan Visuel IA',
        'diagnose_visually': 'Diagnostic Visuel', 'upload_photo': 'Télécharger Photo', 'vision_engine': 'Analyse peau/branchies',
        'start_scan': 'Lancer Scan', 'access_dash': 'Accéder au Tableau', 'phone_email': 'Tél/Email', 'get_otp': 'Obtenir code',
        'sys_settings': 'Paramètres Système', 'configure_otp': 'Config. OTP', 'demo_mode': 'Mode Démo',
        'email_gateway': 'Passerelle Email', 'sms_gateway': 'Passerelle SMS', 'save_config': 'Enregistrer', 'back_home': 'Retour',
        'market_global_title': 'Marché Mondial', 'market_global_desc': 'Parcourir fournisseurs internationaux',
        'filter_country': 'Filtrer par Pays', 'filter_species': 'Filtrer par Espèce', 'btn_order': 'Commander',
    },
    'ja': {
        'doc': '総日数 (DOC)', 'feed_consumed': '総飼料消費量 (kg)', 'predict_size': 'サイズ予測',
        'digital_logbook': 'デジタル日誌', 'secure_history': '履歴を保存', 'th_date': '日付', 'th_notes': 'メモ',
        'add_log': '➕ ログ追加', 'sust_tracker': '持続可能性トラッカー', 'eco_eff': 'エコ効率',
        'harvest_weight': '総収穫重量 (kg)', 'water_usage': '水使用量 (m3)', 'gen_report': 'レポート作成',
        'export_compliance': '輸出コンプライアンス', 'intl_markets': '国際市場確認', 'target_region': '対象地域',
        'avg_weight': '平均体重 (g)', 'check_eligibility': '適格性確認', 'visual_scan': 'AIビジュアルスキャン',
        'diagnose_visually': '視覚的診断', 'upload_photo': '写真アップロード', 'vision_engine': '皮膚・エラの分析',
        'start_scan': 'スキャン開始', 'access_dash': 'ダッシュボードへ', 'phone_email': '電話/メール', 'get_otp': 'OTP取得',
        'sys_settings': 'システム設定', 'configure_otp': 'OTP設定', 'demo_mode': 'デモモード',
        'email_gateway': 'メールゲートウェイ', 'sms_gateway': 'SMSゲートウェイ', 'save_config': '保存', 'back_home': 'ホームへ',
        'market_global_title': 'グローバル市場', 'market_global_desc': '国際サプライヤーを閲覧',
        'filter_country': '国でフィルター', 'filter_species': '魚種でフィルター', 'btn_order': '注文する',
    },
    'te': {
        'doc': 'మొత్తం రోజులు (DOC)', 'feed_consumed': 'మొత్తం ఆహారం (kg)', 'predict_size': 'సైజు అంచనా',
        'digital_logbook': 'డిజిటల్ లాగ్‌బుక్', 'secure_history': 'సురక్షిత చరిత్ర', 'th_date': 'తేదీ', 'th_notes': 'గమనికలు',
        'add_log': '➕ లాగ్ జోడించు', 'sust_tracker': 'స్థిరత్వం ట్రాకర్', 'eco_eff': 'పర్యావరణ సామర్థ్యం',
        'harvest_weight': 'పంట బరువు (kg)', 'water_usage': 'నీటి వినియోగం (m3)', 'gen_report': 'నివేదిక',
        'export_compliance': 'ఎగుమతి నిబంధనలు', 'intl_markets': 'అంతర్జాతీయ మార్కెట్లు', 'target_region': 'లక్ష్య ప్రాంతం',
        'avg_weight': 'సగటు బరువు (g)', 'check_eligibility': 'అర్హత తనిఖీ', 'visual_scan': 'AI విజన్ స్కాన్',
        'diagnose_visually': 'దృశ్య నిర్ధారణ', 'upload_photo': 'ఫోటో అప్‌లోడ్', 'vision_engine': 'చర్మం/మొప్పల తనిఖీ',
        'start_scan': 'స్కాన్ ప్రారంభించు', 'access_dash': 'డ్యాష్‌బోర్డ్', 'phone_email': 'ఫోన్/ఈమెయిల్', 'get_otp': 'OTP పొందండి',
        'sys_settings': 'సిస్టమ్ సెట్టింగులు', 'configure_otp': 'OTP ఆకృతీకరణ', 'demo_mode': 'డెమో మోడ్',
        'email_gateway': 'ఈమెయిల్ గేట్‌వే', 'sms_gateway': 'SMS గేట్‌వే', 'save_config': 'సేవ్ చేయండి', 'back_home': 'తిరిగి వెళ్ళు',
        'market_global_title': 'గ్లోబల్ మార్కెట్', 'market_global_desc': 'అంతర్జాతీయ సరఫరాదారులు',
        'filter_country': 'దేశం వారీగా', 'filter_species': 'రకం వారీగా', 'btn_order': 'ఆర్డర్ చేయండి',
    }
}

def apply_real_translations():
    # Read the file
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    current_lang = None
    
    lang_pattern = re.compile(r"^\s+'([a-z]{2})': \{")
    
    for line in lines:
        match = lang_pattern.match(line)
        if match:
            current_lang = match.group(1)
        
        # Check if line contains a key we want to update
        # Format: "        'key': 'value',"
        line_processed = line
        
        if current_lang in TRANSLATION_TWEAKS:
            key_match = re.search(r"^\s+'([^']+)':", line)
            if key_match:
                key = key_match.group(1)
                if key in TRANSLATION_TWEAKS[current_lang]:
                    val = TRANSLATION_TWEAKS[current_lang][key]
                    # Preserve indentation
                    line_processed = f"        '{key}': '{val}',\n"
                    # Remove from dict so we know we used it (optional, for debugging)
                    # print(f"Updated {current_lang}.{key}")

        new_lines.append(line_processed)
        
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Real translations applied.")

if __name__ == "__main__":
    apply_real_translations()
