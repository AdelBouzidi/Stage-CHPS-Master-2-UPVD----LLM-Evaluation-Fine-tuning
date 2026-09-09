program even_odd_count_demo
  implicit none
  integer :: num
  integer :: even_count, odd_count
  character(len=10) :: str
  integer :: i
  integer :: digit

  ! Read input number
  read(*,*) num

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Convert to string and process each digit
  write(str, '(I0)') abs(num)
  do i = 1, len_trim(str)
    digit = iachar(str(i:i))
    if (iand(digit, 1) == 0) then
      even_count = even_count + 1
    else
      odd_count = odd_count + 1
    end if
  end do

  ! Output results
  print *, even_count, odd_count

end program even_odd_count_demo