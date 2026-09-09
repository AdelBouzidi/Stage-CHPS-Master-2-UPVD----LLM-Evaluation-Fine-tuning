program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer :: i
  character(len=1) :: digit
  character(len=20) :: str

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert number to string (use absolute value for negative numbers)
  str = int_to_string(abs(num))

  ! Process each digit
  do i = 1, len(str)
    digit = str(i:i)
    if (digit == '0' .or. digit == '2' .or. digit == '4' .or. digit == '6' .or. digit == '8') then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  ! Output results
  print *, even_count, odd_count

contains

  function int_to_string(num) result(str)
    integer, intent(in) :: num
    character(len=20) :: str
    write(str, '(I0)') num
  end function int_to_string

end program even_odd_count_demo