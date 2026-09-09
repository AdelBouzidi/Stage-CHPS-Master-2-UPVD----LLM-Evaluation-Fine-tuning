program even_odd_count
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=1) :: digit
  character(len=10) :: num_str

  ! Read input number
  read(*,*) num

  ! Convert to string to process digits
  write(num_str,*) abs(num)

  even_count = 0
  odd_count = 0

  do i = 1, len(num_str)
    digit = num_str(i:i)
    if (ichar(digit) == ichar('0') .or. ichar(digit) == ichar('2') .or. &
        ichar(digit) == ichar('4') .or. ichar(digit) == ichar('6') .or. &
        ichar(digit) == ichar('8')) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  print *, even_count, odd_count

end program even_odd_count