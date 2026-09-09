program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=12) :: str
  integer :: i
  character(len=1) :: digit

  ! Read input number
  read(*,*) num

  ! Get absolute value for digit counting
  num = abs(num)

  ! Convert to string
  write(str, '(I0)') num

  ! Count even and odd digits
  even_count = 0
  odd_count = 0
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

end program even_odd_count