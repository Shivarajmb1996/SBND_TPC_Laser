/****************************************************************************
** Meta object code from reading C++ file 'GUI_schema.h'
**
** Created: Fri Jun 7 12:25:05 2013
**      by: The Qt Meta Object Compiler version 62 (Qt 4.6.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "GUI_schema.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'GUI_schema.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.6.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_MyWidget[] = {

 // content:
       4,       // revision
       0,       // classname
       0,    0, // classinfo
      14,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      10,    9,    9,    9, 0x09,
      42,    9,    9,    9, 0x09,
      64,    9,    9,    9, 0x09,
      79,    9,    9,    9, 0x09,
      91,    9,    9,    9, 0x09,
     115,    9,    9,    9, 0x09,
     134,    9,    9,    9, 0x09,
     154,    9,    9,    9, 0x09,
     174,    9,    9,    9, 0x09,
     190,    9,    9,    9, 0x09,
     206,    9,    9,    9, 0x09,
     222,    9,    9,    9, 0x09,
     244,  238,    9,    9, 0x09,
     266,  238,    9,    9, 0x09,

       0        // eod
};

static const char qt_meta_stringdata_MyWidget[] = {
    "MyWidget\0\0EvenAllowedForDownsampling(int)\0"
    "slotChangeGrp3State()\0Monitor_Mode()\0"
    "Daq_start()\0Oscilloscope_RT_start()\0"
    "Imaging_RT_start()\0GetVoltageCathode()\0"
    "SetVoltageCathode()\0GetVoltageInd()\0"
    "SetVoltageInd()\0GetVoltageCol()\0"
    "SetVoltageCol()\0value\0PostTriggerRange(int)\0"
    "RunNumberCheck(int)\0"
};

const QMetaObject MyWidget::staticMetaObject = {
    { &QWidget::staticMetaObject, qt_meta_stringdata_MyWidget,
      qt_meta_data_MyWidget, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &MyWidget::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *MyWidget::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *MyWidget::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_MyWidget))
        return static_cast<void*>(const_cast< MyWidget*>(this));
    return QWidget::qt_metacast(_clname);
}

int MyWidget::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: EvenAllowedForDownsampling((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: slotChangeGrp3State(); break;
        case 2: Monitor_Mode(); break;
        case 3: Daq_start(); break;
        case 4: Oscilloscope_RT_start(); break;
        case 5: Imaging_RT_start(); break;
        case 6: GetVoltageCathode(); break;
        case 7: SetVoltageCathode(); break;
        case 8: GetVoltageInd(); break;
        case 9: SetVoltageInd(); break;
        case 10: GetVoltageCol(); break;
        case 11: SetVoltageCol(); break;
        case 12: PostTriggerRange((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 13: RunNumberCheck((*reinterpret_cast< int(*)>(_a[1]))); break;
        default: ;
        }
        _id -= 14;
    }
    return _id;
}
QT_END_MOC_NAMESPACE